def ppm_to_ugm3(num: float, mw: float, coeff=40.8862) -> float:
    try:
        return num * mw * coeff

    except Exception as e:
        raise Exception("Failed to convert ppm to ug/m3", e)


def ppb_to_ugm3(num: float, mw: float, coeff=40.8862) -> float:
    try:
        return num * mw * coeff/1000

    except Exception as e:
        raise Exception("Failed to convert ppb to ug/m3", e)


def gsec_to_tyr(num: float, secs=3600, hrs=24, days=365, g_to_tonne=1_000_000):
    try:
        return (num * secs * hrs * days)/g_to_tonne

    except Exception as e:
        raise Exception("Failed to convert g/s to tonnes/year", e)