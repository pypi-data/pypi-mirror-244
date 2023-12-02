from typing import *
from string import Formatter

import listorm

from ..lib import fsave, fbasename, fjoin, select_kwargs



def _get_format_kwargs(formatstr):
    formatter = Formatter()
    return [
        kw for _, kw, _, _ in formatter.parse(formatstr)
    ]



def pipe2file(basedir, subdir:Union[Callable, str]=None):
    '''
    pipe2file(RESULTS_PATH, "{titleName}({titleId})/thumbnail")
    :param subdir: lamabda response, **context: return dir, defaults to None
    '''
    if isinstance(subdir, str):
        format_args = _get_format_kwargs(subdir)
    
    def pipe(results, response, context):
        if subdir:
            if isinstance(subdir, str):
                kwargs = listorm.asselect(context, format_args)
                save_dir = subdir.format(**kwargs)
                save_path = fjoin(basedir, save_dir, fbasename(response.url))
            elif isinstance(subdir, Callable):
                save_path = select_kwargs(subdir, response, **context)
                # save_path = subdir(response, **context)
                save_path = fjoin(basedir, save_path)
            else:
                raise ValueError(subdir)
        else:
            save_path = basedir
        fsave(response.content, save_path)

    return pipe