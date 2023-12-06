# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains helper methods for dataprep."""

import sys

MIN_DATAPREP_VERSION = '1.1.29'
_version_checked = False


def check_min_version():
    global _version_checked
    if _version_checked:
        return
    _version_checked = True
    from pkg_resources import parse_version, get_distribution
    import logging
    installed_version = get_distribution('azureml-dataprep').version
    if parse_version(installed_version) < parse_version(MIN_DATAPREP_VERSION):
        logging.getLogger().warning(
            _dataprep_incompatible_version_error.format(MIN_DATAPREP_VERSION, installed_version))


def is_dataprep_installed():
    try:
        from azureml.dataprep import api
        return api is not None
    except Exception:
        return False


def dataprep():
    if not is_dataprep_installed():
        raise ImportError(get_dataprep_missing_message())
    import azureml.dataprep as _dprep
    check_min_version()
    return _dprep


def dataprep_fuse():
    try:
        import azureml.dataprep.fuse.dprepfuse as _dprep_fuse
        check_min_version()
        return _dprep_fuse
    except ImportError:
        raise ImportError(get_dataprep_missing_message(extra='[fuse]'))


def ensure_dataflow(dataflow):
    if not isinstance(dataflow, dataprep().Dataflow):
        raise RuntimeError('dataflow must be instance of azureml.dataprep.Dataflow')


def update_metadata(dataflow, action, source, **kwargs):
    from copy import deepcopy
    meta = deepcopy(dataflow._meta)

    if 'activityApp' not in meta:
        meta['activityApp'] = source

    if 'activity' not in meta:
        meta['activity'] = action

    try:
        import os
        run_id = os.environ.get("AZUREML_RUN_ID", None)
        if run_id is not None:
            meta['runId'] = run_id  # keep this here so not to break existing reporting
            meta['run_id'] = run_id
    except Exception:
        pass

    if len(kwargs) > 0:
        kwargs.update(meta)
        meta = kwargs
    return meta


def get_dataflow_for_execution(dataflow, action, source, **kwargs):
    return dataflow._copy_and_update_metadata(action, source, **kwargs)


def get_dataflow_with_meta_flags(dataflow, **kwargs):
    if len(kwargs) > 0:
        return dataflow._copy_and_update_metadata(None, None, **kwargs)
    return dataflow


def get_dataprep_missing_message(issue=None, extra=None, how_to_fix=None):
    dataprep_available = sys.maxsize > 2**32  # no azureml-dataprep available on 32 bit
    extra = extra or ''
    if how_to_fix:
        suggested_fix = ' This can {}be resolved by {}.'.format('also ' if dataprep_available else '', how_to_fix)
    else:
        suggested_fix = ''

    message = (issue + ' due to missing') if issue else 'Missing'
    message += ' required package "azureml-dataset-runtime{}", which '.format(extra)

    if not dataprep_available:
        message += 'is unavailable for 32bit Python.'
    else:
        message += 'can be installed by running: {}'.format(_get_install_cmd(extra))

    return message + suggested_fix


def is_tabular(transformations):
    tabular_transformations = {
        'Microsoft.DPrep.ReadParquetFileBlock',
        'Microsoft.DPrep.ParseDelimitedBlock',
        'Microsoft.DPrep.ParseJsonLinesBlock'
    }

    file_transformations = {
        'Microsoft.DPrep.ToCsvStreamsBlock',
        'Microsoft.DPrep.ToParquetStreamsBlock',
        'Microsoft.DPrep.ToDataFrameDirectoryBlock'
    }

    def r_index(collection, predicate):
        for i in range(len(collection) - 1, -1, -1):
            if predicate(collection[i]):
                return i
        return -1

    steps = transformations._get_steps()
    tabular_index = r_index(steps, lambda s: s.step_type in tabular_transformations)
    file_index = r_index(steps, lambda s: s.step_type in file_transformations)

    return tabular_index > file_index


def _get_install_cmd(extra):
    return '"{}" -m pip install azureml-dataset-runtime{} --upgrade'.format(sys.executable, extra or '')


_dataprep_incompatible_version_error = (
    'Warning: The minimum required version of "azureml-dataprep" is {}, but {} is installed.'
    + '\nSome functionality may not work correctly. Please upgrade it by running:'
    + '\n' + _get_install_cmd('[fuse,pandas]')
)


def dataprep_stub():
    """
    Returns a stub of azureml.dataprep module that allows constructing v1 json based dataflows
    without the need for dataprep engine.
    """
    import azureml.data._dataprep_stub as _stub
    return _stub
