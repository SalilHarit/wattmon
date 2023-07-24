from matplotlib import pyplot as plt
import psycopg2
import PyQt5.QtWidgets as qtw
import matplotlib.backends.backend_qt5agg as plt_qt5

# Connect to the PostgreSQL database.
conn = psycopg2.connect(host="localhost", database="wattmon", user="wattmon", password="password")

# Create a cursor.
cur = conn.cursor()

# Query the database for the solar generation data.
cur.execute("SELECT date_hour, wind_speed, sunshine, air_pressure, radiation, air_temperature, relative_air_humidity, system_production  FROM solar_data_2")

# Fetch the results of the query.
results = cur.fetchall()

# Create a list of lists to store the data for each graph.
graphs = []
for i in range(8):
    graph = []
    for row in results:
        graph.append(row[i])
    graphs.append(graph)

# Create a Qt application.
app = qtw.QApplication([])

# Create a Qt FigureCanvas.
canvas = plt_qt5.FigureCanvasQTAgg(plt.figure())

# Plot the graphs in the Qt FigureCanvas.
for i in range(8):
    plt.plot(graphs[i])
    plt.xlabel("Date")
    plt.ylabel(f"{graphs[i][0]}")
    plt.title(f"Graph {i + 1}")
    canvas.draw()

# Create a Qt MainWindow.
w = qtw.QMainWindow()
w.setWindowTitle("Solar Generation")

# Set the central widget of the Qt MainWindow.
w.setCentralWidget(canvas)

# Show the Qt MainWindow.
w.show()

# Start the Qt event loop.
app.exec_()

# Close the cursor and the connection.
cur.close()
conn.close()
