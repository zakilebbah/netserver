from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # SocketIO.run(app, host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0')