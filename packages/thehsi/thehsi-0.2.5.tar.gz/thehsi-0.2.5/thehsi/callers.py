from importlib import import_module
from thehsi import CallData, Kernel
from os import listdir, mkdir
from os.path import exists

def is_module_valid(module):
    valid_chars: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    return not bool(
        len(
            list(
                filter(
                    lambda x : x,
                    [not i in valid_chars for i in module]
                )
            )
        )
    )

def load_callers(application_path: str):
    application_path: str = str(
        application_path.replace(
            "\\",
            "/"
        ) # Windows Support
    )

    if not exists(
        f"{application_path}/"
    ):
        print("[ERROR]: The Path you entered does not exist!")
        exit()

    if not exists(
        f"{application_path}/applications/"
    ):
        print("[INFO]: No 'application' folder found! Creating...")
        mkdir(f"{application_path}/applications/")
    
    applications: list[str] = []
    applications: list[str] = list(
        listdir(
            f"{application_path}/applications/"
        )
    )

    callers: dict[dict] = {}

    for application in applications:
        if not is_module_valid(application):
            print(f"[WARNING]: Application '{application}' could not be loaded!\n  The application has an invalid name\n")
            continue
        
        if not exists(
            f'{application_path}/applications/{application}/__hmgr_caller__.py'
        ): continue

        application_caller = import_module(
            f'applications.{application}.__hmgr_caller__'
        )

        if not hasattr(application_caller, 'kernel'):
            print(f"[WARNING]: Application '{application}' could not be loaded!\n  Invalid __hmgr_caller__.py! No Kernel imported\n  Make sure the Kernel is in a variable called 'kernel'")
            continue

        kernel: Kernel = application_caller.kernel
        if kernel.app_id != application:
            print(f"[WARNING]: Application '{application}' could not be loaded!\n  The application folder name must match the id\n")
            continue
        application_callers: dict = kernel.__callers__
        for caller_key in application_callers.keys():
            caller = application_callers[caller_key]
            callers[
                f"{caller['application_id']}:{caller_key}"
            ] = caller

    return callers

def call(callers: dict, caller_key: str, args: list = []):
    if not caller_key in callers:
        print(f"[ERROR]: Cannot Call '{caller_key}'\n  No such call\n")
        return
    call_data: CallData = CallData()
    caller: dict = callers[caller_key]
    func: callable = caller['function']
    return func(call_data, args)