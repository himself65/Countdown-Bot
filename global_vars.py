try:
    import config
except ModuleNotFoundError as ex:
    import config_default as config

registered_commands = {

}

message_listeners = [

]
last_message = None
repeat_time = 0
