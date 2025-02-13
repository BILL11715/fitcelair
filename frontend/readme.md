# Frontend for Streaming application

## requirements :

- `python 3.12 or higher`
- `mongodb` for database
- `vscode or other text editor`
- `git`
- `yahoo finance Account` to call all data tickers with your API_KEY

## steps

If you don't want to use `virtual environment`,you can skip `steps 3` below.<br>
Thanks for your best comprehension.<br>

If you have your `API_KEY` of `yfinance` account please paste it on `API_KEY.txt` file on the root folder of project

This is the steps to run application correctly:

1. Before running application you must save all data form tickers in your mongodb database.
   To do it,you can use playground of mongodb extension on vscode.
   call your database "streaming_db" and your collection "stocks" inside of "streaming_db" database.

2. Clone project with git use command :

   ```cmd
      $ git clone https://github.com/UlrichIvan/frontend_streaming_app.git
   ```

3. Create the virtual `environment` for your project using command below:

   ```cmd
      $ python -m venv .env
   ```

   if you use cli inside of vscode it will detect the creation of the virtual environment.
   then accept the proposition on vscode on right bottom interface the click ok.

4. Download all required packages with this command below:

   ```cmd
      $ pip -install -r requirements.txt
   ```

   `Requirements.txt` is the file at the root folder of project that contains list of packages using from project just run the command below and python will be install all required packages for you.

5. Run the mongodb service.<br/>
   If you use linux `ubuntu` platform run this command below:

   ```cmd
      $ systemctl start mongo.service
   ```

   After it if you not the root user, you will enter your password and press enter.
   if you use other linux distribution or other platform like window or macos ,please search on your `navigator` how you can run mongodb service,you will receive the answer about it.<br>
   Thanks.

6. After running mongodb service,run the application with command below:

   ```cmd
      $ streamlit run main.py
   ```

   this command line will run your streamlit application on your default browser or specific port.<br>
   By default streamlit run your application on (http://localhost:8501)

After it you will see you application running on (http://localhost:8501) in your browser.

Thanks for your attention and your time waited to run this application.
