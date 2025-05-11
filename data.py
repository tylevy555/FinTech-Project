import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

year = 2024

savor = pd.read_csv('Statement-SavorOne2024.csv', encoding='unicode_escape')
venture = pd.read_csv('Statement-VentureOne2024.csv', encoding='unicode_escape')
combined = savor + venture

savor.head()
venture.head()