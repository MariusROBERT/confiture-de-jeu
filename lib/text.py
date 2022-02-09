def rect_size_floating(dimension_min : tuple, c : float, x : int, N : int):
    """[summary]

    Args:
        dimension_min (tuple): (T,T) taille min du rectangle
        c (int): coef taille max
        x (int): numero image
        N (int): nombre d'image

    Returns:
        [type]: dimension
    """
    
    dimension_output = []
    if x <= N/2:
        for T in dimension_min:
            a = (c * T - T) / (N/2)
            dimension_output.append(a*x + T)
    else:
        x = x - N/2
        for T in dimension_min:
            a = (T - c * T) / (N/2)
            dimension_output.append(a*x + c*T)
    return dimension_output
