# Live-Exceptions
A Django middleware that logs exceptions to database

## Using Live-Exceptions
To use this middleware, all you need to do to is edit your django settings.
```
MIDDLEWARE_CLASSES = [
    ...
    
    // Make sure to use the middleware close or preferrably to the end of the MIDDLEWARE_CLASSES stack.
    'path.to.liveexceptions.middleware.LiveExceptionMiddleware',
]
```

Please do note that the middleware source can live anywhere in the python path.
