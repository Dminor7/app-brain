# App-Brain-Scrapper

Scrapping stats of applications for given google-play-developer URLs.

## Getting Started

There is a GUI application : `AppBrain.exe` that you can directly use and for customization you can configure the scripts.

### Prerequisites

* Need <b>premium</b> account of AppBrain. Currently only *sign-in with google* feature is available.

* `Chrome and chromedriver version 81`. (You can use chromedriver version according to your Chrome version, just replace the `chromedriver.exe`)

* For Customization, using `conda` make an enviornment with `enviornment.yml` file.


    ```
    conda env create -f environment.yml
    ```

### Files

* `main.py` contains the GUI event loop that triggers the `crawl` method.

* `login.py` contains the functionality of login with AppBrain. You can add here methods for login with `facebook`, `twitter` and standard `App Brain` login. Currently only Sign-In with Google is supported.

* Make an `input.csv` file here you have to input URLs in format like `https://play.google.com/store/apps/developer?id={developerId}` and the header for the file is `urls`.

* `spider.py`contains the main crawling method, for every given developer accounts it finds the developer's applications list and crawl. 

* `detail_page.py` contains the method of scraping every element for the detail application page.

* `utils.py` contains the xpath and css-selector for each element you want to scrape.

* `log.py` provides the logger object with DEBUG level

* `output` folder will be created containing the CSV files for respective Developer account.

## Building Executable

After customizing scripts, if you want to build the executable. Activate the enviornment using 

```bash
conda env create -f environment.yml
activate env  
```

After activating run 
```bash
auto-py-to-exe
```
A GUI window will open,
setup configuration for your application

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


