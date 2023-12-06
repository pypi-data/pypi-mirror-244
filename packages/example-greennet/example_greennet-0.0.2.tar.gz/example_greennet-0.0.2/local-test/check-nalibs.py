from nalibs import load_json, intialize_logging

print(load_json("./exam01.json"))

DEBUG = False
log = intialize_logging(DEBUG)

log.debug("hello debug")
log.info("hello info")
log.error("hello error")
log.warning("hello warning")
