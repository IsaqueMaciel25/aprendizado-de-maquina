# Importação das bibliotecas necessárias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Passo 1: Coleta de Dados
# Carregando um conjunto de dados fictícios
data = pd.read_csv('customer_data.csv')

# Passo 2: Pré-processamento dos Dados
# Verificando valores nulos e preenchendo se necessário
data = data.fillna(method='ffill')

# Separando as características (X) e o alvo (y)
X = data.drop('Purchase', axis=1)
y = data['Purchase']

# Passo 3: Divisão dos Dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Passo 4: Escolha do Modelo
# Utilizando RandomForestClassifier como exemplo
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Passo 5: Treinamento do Modelo
model.fit(X_train, y_train)

# Passo 6: Avaliação do Modelo
y_pred = model.predict(X_test)

# Exibindo a matriz de confusão, relatório de classificação e acurácia
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))

# Passo 7: Ajuste e Otimização
# (Este exemplo não inclui ajuste de hiperparâmetros, mas você pode usar GridSearchCV ou RandomizedSearchCV para isso)

# Passo 8: Interpretação e Visualização
import matplotlib.pyplot as plt
import seaborn as sns

# Visualizando a importância de cada característica
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
feature_importances.nlargest(10).plot(kind='barh')
plt.show()