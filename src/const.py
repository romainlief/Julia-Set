# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600

# Domaine complexe (par défaut pour Julia; ajustable)
RE_MIN, RE_MAX = -2.0, 2.0
IM_MIN, IM_MAX = -2.0, 2.0

# Paramètre constant c du Julia set
# Valeur classique: c = -0.7 + 0.27015j
C_RE, C_IM = -0.7, 0.27015

# Bornes des sliders pour Re(c) et Im(c)
# Modifie-les pour contrôler la plage explorée
C_RE_MIN, C_RE_MAX = -1.5, 1.5
C_IM_MIN, C_IM_MAX = -1.5, 1.5

# Pos interessantes pour c
POSIx1 = 0.4903104314051678 + 0.4903117169556031 / 2
POSIy1 = 0.004602709742604857 + 0.004603995293040264 / 2