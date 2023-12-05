import logging
import pygogo
import traceback
import os
from pathutility import PathUtils
pu=PathUtils()

def create_file_formatter(uri_log):
    """
        Creates a csv file for log with the headers
    """
    # To get path exclude file name
    pu.create_directory_if_not_exists(pu.get_parent_directory(uri_log))

    # If log don't exist create headers
    if not os.path.isfile(uri_log):
        with open(uri_log, mode="w") as file:
            file.write("; ".join(['Fecha', 'Modulo', 'File', 'Función', 'Linea', 'Descripción', 'Tipo Error', 'Error']))
            file.write("\n")

    return logging.FileHandler(uri_log)

def transform_error(**kwargs_in):
    """
    Función que sirve para procesar los parametros de una excepcion.
    :param kwargs_in: Keys del diccionario.
            'error': mensaje de excepcion
            'description': narrativa escrita por el usuario para tener mejor comprensión del error del programa

    :return: diccionario con los siguientes parametros:
            'func_name': nombre de la función que produce la excepción.
            'error_name': nombre del tipo de error.
            'error': descriptivo del error.
            'error_line': línea de código dónde se produce el error
            'description': narrativa escrita por el usuario para tener mejor comprensión del error del programa.
    """

    kwargs_out = {
        "file_name": "",
        "func_name": "",
        "error_line": "",
        "error_name": "",
        "error": "",
        "description": ""
    }

    if "error" in kwargs_in.keys():
        stack_info = traceback.extract_tb(kwargs_in['error'].__traceback__)[-1]
        kwargs_out['file_name'] = f'{pu.get_filename(stack_info[0])}'
        kwargs_out['func_name'] = stack_info[2]
        kwargs_out['error_line'] = stack_info[1]
        kwargs_out["error_name"] = kwargs_in["error"].__class__.__name__
        kwargs_out["error"] = str(kwargs_in["error"]).replace("\n", " | ").replace(";", ":")

    if "description" in kwargs_in.keys():
        kwargs_out["description"] = kwargs_in['description']

    return kwargs_out


def log_error(module, file_path, **kwargs_msg):
    """
    Función que genera un log de errores.

    :param module: nombre del script y modulo que genera el error
    :param file_path: ruta dónde se generará el archivo de errores
    :param kwargs_msg:
            'error': excepción generada
            'description': narrativa escrita por el usuario para tener mejor comprensión del error del programa.
    """
    logging_fmt = '%(asctime)s;%(name)s;%(message)s'
    fmttr = logging.Formatter(logging_fmt, datefmt=pygogo.formatters.DATEFMT)
    fhdlr = create_file_formatter(file_path)

    logger = pygogo.Gogo(name=module, high_hdlr=fhdlr, high_formatter=fmttr, monolog=True).get_logger("py")

    kwargs_error = transform_error(**kwargs_msg)

    msg = "{file_name};{func_name};{error_line};{description};{error_name};{error}".format(**kwargs_error)

    if len(logger.handlers) > 2:
        logger.handlers.pop(0)
    logger.error(msg)

    for hdlr in logger.handlers:
        hdlr.close()
        logger.removeHandler(hdlr)