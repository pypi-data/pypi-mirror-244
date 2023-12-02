"""Pipeline anomaly dimension classification."""


class Error(Exception):
    """Feature Class exception."""


class FeatureClass:
    """Class for given geometry parameters."""

    AXGR = 'AXGR'  # Axial Grooving
    AXSL = 'AXSL'  # Axial Slotting
    CIGR = 'CIGR'  # Circumferential Grooving
    CISL = 'CISL'  # Circumferential Slotting
    GENE = 'GENE'  # General
    PINH = 'PINH'  # Pinhole
    PITT = 'PITT'  # Pitting


def size_class(length, width, thick):
    """Calculate feature class for given parameters."""
    if not all([width, length, thick]):
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    size1 = max(thick, 10)
    size3 = 3 * size1
    size6 = 6 * size1
    lwr = float(length) / float(width)

    if (width >= size3) and (length >= size3):
        ret = FeatureClass.GENE

    elif (
      (size6 > width >= size1) and
      (size6 > length >= size1) and
      (2.0 > lwr > 0.5)
    ) and not (width >= size3 <= length):
        ret = FeatureClass.PITT

    elif (size3 > width >= size1) and (lwr >= 2.0):
        ret = FeatureClass.AXGR

    elif (size3 > length >= size1) and (lwr <= 0.5):
        ret = FeatureClass.CIGR

    elif (size1 > width > 0) and (size1 > length > 0):
        ret = FeatureClass.PINH

    elif length >= size1 > width > 0:
        ret = FeatureClass.AXSL

    elif width >= size1 > length > 0:
        ret = FeatureClass.CISL

    else:
        raise Error("Wrong FeatureClass params. l={} w={} t={}".format(length, width, thick))

    return ret
