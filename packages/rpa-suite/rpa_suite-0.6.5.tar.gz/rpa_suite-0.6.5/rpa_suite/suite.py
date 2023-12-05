from .clock.waiter import wait_for_exec
from .clock.exec_while import exec_wtime
from .date.date import get_hms, get_dma
from .email.sender_smtp import send_email
from .file.counter import count_files
from .file.temp_dir import create_temp_dir, delete_temp_dir
from .log.loggin import logging_decorator
from .log.printer import alert_print, success_print, error_print, info_print, print_call_fn, print_retur_fn, magenta_print, blue_print
# from .regex.list_from_text import create_list_using_regex
from .validate.mail_validator import valid_emails
from .validate.string_validator import search_in

class Rpa_suite():
    wait_for_exec = wait_for_exec
    exec_wtime = exec_wtime
    get_hms = get_hms
    get_dma = get_dma
    send_email = send_email
    count_files = count_files
    create_temp_dir = create_temp_dir
    delete_temp_dir = delete_temp_dir
    alert_print = alert_print
    success_print = success_print
    error_print = error_print
    info_print = info_print
    print_call_fn = print_call_fn
    print_retur_fn = print_retur_fn
    magenta_print = magenta_print
    blue_print = blue_print
    # create_list_using_regex = create_list_using_regex()
    valid_emails = valid_emails
    search_in = search_in
    
rpa = Rpa_suite()

def invoke(Rpa_instance):
    return Rpa_instance

invoke(rpa)
