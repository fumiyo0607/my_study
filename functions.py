import numpy as np

# affine関数
def affine(X, W, b):
    return np.dot(X, W) + b

# ReLu関数
def relu(x):
    return np.maximum(0, x)

# soft_max関数
def soft_max(x):
    max_x = np.max(x, axis=1,keepdims=True)
    exp_x = np.exp(x-max_x)
    y = exp_x/np.sum(exp_x, axis=1, keepdims=True)
    return y

