import matplotlib.pyplot as plt

def plot_grafico_linear(x, y, xlabel="X", ylabel="Y", title="Gráfico Linear"):
    """
    Plota um gráfico linear.

    Parâmetros:
    - x (array-like): Dados para o eixo X.
    - y (array-like): Dados para o eixo Y.
    - xlabel (str): Rótulo do eixo X (padrão: "X").
    - ylabel (str): Rótulo do eixo Y (padrão: "Y").
    - title (str): Título do gráfico (padrão: "Gráfico Linear").

    Retorna:
    - None
    """
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_grafico_de_dispersao(x, y, xlabel="X", ylabel="Y", title="Gráfico de Dispersão"):
    """
    Plota um gráfico de dispersão.

    Parâmetros:
    - x (array-like): Dados para o eixo X.
    - y (array-like): Dados para o eixo Y.
    - xlabel (str): Rótulo do eixo X (padrão: "X").
    - ylabel (str): Rótulo do eixo Y (padrão: "Y").
    - title (str): Título do gráfico (padrão: "Gráfico de Dispersão").

    Retorna:
    - None
    """
    plt.scatter(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_grafico_de_barra(x, y, xlabel="X", ylabel="Y", title="Gráfico de Barra"):
    """
    Plota um gráfico de barra.

    Parâmetros:
    - x (array-like): Rótulos das categorias.
    - y (array-like): Alturas das barras correspondentes.
    - xlabel (str): Rótulo do eixo X (padrão: "X").
    - ylabel (str): Rótulo do eixo Y (padrão: "Y").
    - title (str): Título do gráfico (padrão: "Gráfico de Barra").

    Retorna:
    - None
    """
    plt.bar(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_grafico_de_pizza(labels, sizes, title="Gráfico de Pizza"):
    """
    Plota um gráfico de pizza.

    Parâmetros:
    - labels (list): Rótulos para as fatias da pizza.
    - sizes (list): Tamanhos relativos das fatias.
    - title (str): Título do gráfico (padrão: "Gráfico de Pizza").

    Retorna:
    - None
    """
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assegura que o gráfico de pizza é desenhado como um círculo.
    plt.title(title)
    plt.show()
