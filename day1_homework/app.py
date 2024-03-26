from flask import Flask
from flask import request

import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



quotes = [
    {
        "id":       1
        ,"author":  "Rick Cook"
        ,"text":    "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
        ,"rating":  1
    },

    {
        "id":       2
        ,"author":  "Waldi Ravens"
        ,"text":    "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
        ,"rating":  1
    },

    {
        "id":       3
        ,"author":   "Mosher’s Law of Software Engineering"
        ,"text":     "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
        ,"rating":  1
    },

    {
        "id":       4
        ,"author":   "Yoggi Berra"
        ,"text":     "В теории, теория и практика неразделимы. На практике это не так."
        ,"rating":  1
    },
]



about_me = {
    "name": "Евгений",
    "surname": "Юрченко",
    "email": "eyurchenko@specialist.ru"
    }


#Практика: Часть 2. доп задание п.2
@app.route("/quotes/filter", methods=['GET'])
def search_quotes():
    result_list = []
    args = request.args
    
    author = args.get('author')
    rating = int(args.get('rating'))

    for quote in quotes:
        if (None not in (author, rating)) and quote['author'] == author and quote['rating'] == rating:
            result_list.append(quote)
        
        elif (author is not None) and quote['author'] == author:
            result_list.append(quote)

        elif (rating is not None) and (quote["rating"] == rating):
            result_list.append(quote)

    return result_list, 200   




#Практика: Часть 2. Задание 5
@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete(quote_id):
    for quote in quotes:
    
        if quote['id'] == quote_id:
            quotes.remove(quote)  
 
            return f"Quote with id {quote_id} is deleted.", 200
        
    return f"Quote with id={quote_id} not found", 404




#Практика: Часть 2. Задание 4
@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    new_data = request.json
    for quote in quotes:
    
        if quote['id'] == quote_id:   
            if  "author" in new_data:
                quote["author"] = new_data["author"]
        
            if  "text" in new_data:
                quote["text"] = new_data["text"]

            if  "rating" in new_data:
                quote["rating"] = min(new_data["rating"], 5)

            return quote
        
    return f"Quote with id={quote_id} not found", 404



def get_new_quote_id():
    return quotes[-1]["id"] + 1


#Практика: Часть 2. доп задание п.1
def add_new_quote(json_request):
    
    new_quote = json_request.copy()
    new_quote["id"] = get_new_quote_id() 
    
    if not ("rating" in new_quote):
        new_quote["rating"] = 1
    else:
        new_quote["rating"] = min(new_quote["rating"], 5)

    return new_quote



#Практика: Часть 2. Задание 3
@app.route("/quotes", methods=['POST'])
def add_quote():
   
   new_quote = add_new_quote(request.json)
   quotes.append(new_quote)

   return new_quote, 201



#Практика: Часть 1. Задание 4
@app.route("/random")
def show_random():
    return quotes[random.randint(0, len(quotes) - 1)]

                 
#Практика: Часть 1. Задание 3
@app.route("/count")
def show_count():
    return {
           "count " : str(len(quotes))
        }


#Практика: Часть 1. Задание 1 и Задание 2
@app.route('/quotes/<int:quota_id>')
def show_quota(quota_id):
    for quota in quotes:
        if quota['id'] == quota_id:   
            return quota
    
    return f"Quote with id={quota_id} not found", 404


@app.route("/quotes")
def show_quotes():
    return quotes


@app.route("/about")
def about():
    return about_me


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)

