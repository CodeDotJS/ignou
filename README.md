# IGNOU Term End Result Viewer

The IGNOU Term End Result Viewer is a web application built with Flask that allows users to fetch and view their term-end examination results from the result portal of Indira Gandhi National Open University.

<p align="center"><img width="80%" src="media/ignou.jpg" alt=""></p>

<p align="center"><b>Check out the <a href="https://ignoux.vercel.app">live</a> version.</b></p>

## Features

- Fetch and display term-end examination results by providing the session and enrollment number, which removes the hassle of finding out the link related to the particular session result.

- Once entered, you don't have to worry about remembering your details.
- Refresh to fetch the latest results without entering any details.
- Delete locally saved data (used for offline viewing) when no longer needed.

## Run

To run the project locally, follow these steps:

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/CodeDotJS/ignou.git
cd ignou
```

2. Install dependencies using pip:


```bash
pip install -r requirements.txt
```

3. Run the Flask application:

```bash
python app.py
```

4. Open your web browser and go to http://localhost:5000 to access the application.

## Plan

It's an on going project where I'll build multiple tools to simplify IGNOU related tasks.

- CLI for IGNOU Term End Result Viewer - [`View`](tools/termendresult.py)

<p align="center"><img src="media/termend.png" alt=""></p>

## License

MIT &copy; Rishi Giri
