import sys
import numpy as np


def dtypecheck(array, filterna=True, float2int=True, show_exceptions=True, dtypes=(np.uint8,
                                                                                   np.int8,
                                                                                   np.uint16,
                                                                                   np.int16,
                                                                                   np.uint32,
                                                                                   np.int32,
                                                                                   np.uint64,
                                                                                   np.int64,
                                                                                   np.uintp,
                                                                                   np.intp,
                                                                                   np.float16,
                                                                                   np.float32,
                                                                                   np.float64,
                                                                                   'M',
                                                                                   'm',
                                                                                   'O',
                                                                                   'P',
                                                                                   'S',
                                                                                   'U',
                                                                                   'V',
                                                                                   'p',
                                                                                   's',
                                                                                   np.complex64,
                                                                                   np.complex128,
                                                                                   np.datetime64,

                                                                                   np.timedelta64,
                                                                                   np.void, bool,
                                                                                   object
                                                                                   )):
    r"""
    Check and convert the data type of a NumPy array based on a predefined set of data types.

    Parameters:
    - array (numpy.ndarray): Input NumPy array.
    - filterna (bool, optional): If True, remove NaN values from the array before type checking.
                                  Default is True.
    - float2int (bool, optional): If True, convert float arrays to integer if they contain only integers.
                                  Default is True.
    - dtypes (tuple, optional): Tuple of NumPy data types to check against. Default includes various numeric,
                               datetime, timedelta, complex, boolean, and object types.

    Returns:
    - numpy.ndarray: NumPy array with the converted data type.

    Examples:
    ```python

        from numpytypechecker import dtypecheck
        import numpy as np
        # Example
        a1D = np.array([1, 2, 3, 4])
        a2D = np.array([[1, 2], [3, 4]])
        a3D = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        b1 = np.array([2., 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9])
        b2 = np.array([[1., 1., 1., 0.],
                       [1., 1., 0., 1.],
                       [0., 0., -3., 0.],
                       [0., 0., np.nan, -4.]])

        print(dtypecheck(a1D, filterna=True, float2int=True, ).dtype)
        print(dtypecheck(a2D, filterna=True, float2int=True, ).dtype)
        print(dtypecheck(a3D, filterna=True, float2int=True, ).dtype)
        print(dtypecheck(b1, filterna=True, float2int=True, ).dtype)
        print(dtypecheck(b2, filterna=False, float2int=True, ).dtype)

        # uint8
        # uint8
        # uint8
        # float64
        # float64

    """
    try:
        arr = array.copy()
        try:
            hasdot = '.' in str(arr.ravel()[0])
        except Exception as fe:
            if show_exceptions:
                sys.stderr.write(f'{fe}\n')
                sys.stderr.flush()
                hasdot = False
        if filterna:
            try:
                arr = arr[~np.isnan(arr)]
            except Exception as ca:
                if show_exceptions:
                    sys.stderr.write(f'{ca}\n')
                    sys.stderr.flush()

        for dty in dtypes:
            try:
                if arr.ndim > 2:
                    littletest = arr[0].astype(dty)
                    _ = np.all(arr == littletest)
                nd = arr.astype(dty)
                if np.all(arr == nd):
                    if not float2int:
                        if hasdot:
                            if '.' in str(arr.ravel()[0]) and '.' not in str(nd.ravel()[0]):
                                continue

                    return array.astype(dty)
            except Exception as fe:
                if show_exceptions:
                    sys.stderr.write(f'{fe}\n')
                    sys.stderr.flush()
        return array
    except Exception as fe:
        if show_exceptions:
            sys.stderr.write(f'{fe}\n')
            sys.stderr.flush()
    return array
