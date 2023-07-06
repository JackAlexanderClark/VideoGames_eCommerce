# Milestone Project 4 – Django Project

### Title: Gallery of the Future

### Author: Jack Clark

### Email: jackalexanderclark@protonmail.com

### Website Link to Heroku App: https://art-gallery-django-5b7a338cde1a.herokuapp.com/

![all-devices-black (2)](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/30dc84c8-5e79-48f1-acb2-e2f9fc71cbb6)

<hr>

## Section 1: Introduction

For my fourth milestone project I have built a Django application in the Pycharm IDE, that utilises several applications such as the gallery, shipping and authentication.

It uses AI generated art-work, using the cutting edge DALLE-2 (https://openai.com/dall-e-2), it can creates images from human text prompts. Attributes such as styles can be applied to mimic artists or effects.

Similar, to CHAT-GPT another OpenAI product it is trained on large quantities of images and studies the relationship between objects.

### A step by step guide through the app

Home Page:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/0841dd76-a60e-42a4-86fb-82133885df15)


Gallery:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/23de3fd5-d708-4ff5-822f-77c620fca3a9)


Hovering on a image:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/84d75dd6-fb44-4f84-a7c2-0b83a6cdf5b0)


Selecting an Image:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/38c14e92-8d04-490a-9ebf-e2ab237460ab)


Add your Orders to the Shopping Basket:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/329c0952-8d41-41e4-93ac-9b4708b767d3)


Remove, Add or Delete the item from your shopping basket:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/58135652-d45a-4d21-bb1c-211b8bdb630c)


Enter Details Page 1 of 3:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/e5354148-9df2-4e8f-8067-9dbe56b501c1)


Bank Details Page 2 of 3:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/32152f05-650e-482b-ae05-fb6d4f93cea7)


Shipping Speed Page 3 of 3:
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/966f363b-ddcd-42c8-8d1c-7e17dab4c7b7)


Confirm Purchase and charge card screen with receipt generated
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/e78eb23e-5990-4271-a51e-ccc2593af33e)


Receipts in profile and shipping statuses with option to edit your user profile
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/2775e88d-db08-4f96-a90b-30649a83b1b8)

<hr>

## Section 2: Project Design and Planning

- The project is a fictional art gallery using AI generated artwork. Users will be able to register an account, login and then browse the homepage which details the ethos and how DALLE-2 works.

- From there Users will be able to view the gallery with contains a variety of artwork, by hovering over and selecting a piece from the gallery – they can choose the piece they want and add it to their shopping basket. The quantities can be edited if they want multiple copies.

- After the User has selected the items they wish to purchase, they are then taken to the shipping section.

- Users can enter their shipping details and their card payments which are stored in their respective SQL models, the payments are handled using the third party “Stripe” API.

- Once the user has chosen their shipping destination, entered their banking details and the shipping speed.

- An order and receipt is generated which is stored within their profile, so they can track all their orders and their statuses.

#### ERD Diagram and Database Scheme
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/17cfa7f9-99f3-44ef-93c5-e6c94c40f035)
- I have arranged the projects logic into two separate applications; gallery and shipping.
- Firstly, gallery will house the majority of the frontend such as the homepage and the shop gallery.
- Users can visit the gallery and click on an image to be taken to a page which will give information such as the price, quantity and description.
- Once items are chosen in the basket and a purchase is confirmed, the


#### Stripe Payment API
- To safely handle payments, the stripe API is used. We can use dummy card details to test.
- Two functions are used, one to generate a card token, that stores the bank details such as account number, sort code and cvv.
- The second function, will charge the card a defined amount in a chosen currency.
- Below is a POST request of the card being charged successfully.

![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/db72a0dc-3f90-49a3-a5b0-84ac9d80e600)

<br>

- Here is the card token being generated when valid card details are provided. As we can see a 200 OK POST request is received meaning the data was successfully transmitted via API.
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/79d7a0db-7778-4423-bf0a-c808758dfce9)


<hr>

## Section 3 - Tech Stack
1. Front-end:
HTML (HyperText Markup Language) serves as the backbone of a website, dictating the structure and content of a web page. By organizing content into different elements like headers, paragraphs, lists, images, and links, HTML provides the basic layout and format for each page. This ties into the DOM (Document Object Model). CSS (Cascading Style Sheets) handles this structure with style and aesthetics. I used it in combination with chrome dev tools to test how an element would look before applying it. 

CSS specifies the visual elements of a web page such as colour, fonts, and layout, allowing for complete control over the design and responsiveness across different devices. Together, HTML and CSS form the static components of a web page, but for an interactive and dynamic user experience.

JavaScript plays a crucial role in making the web interactive, by manipulating HTML and CSS elements based on user inputs and actions. Javascript can target particular elements on the webpage and then manipulate them in different ways, it can also respond to user input. Used for form validation, interactive maps, or dynamic content updates. While HTML, CSS, and JavaScript form the core of frontend web development, libraries and frameworks like Bootstrap make this process more efficient and responsive.

 Bootstrap is a CSS framework that helps in creating visually appealing and responsive designs with minimal effort. It uses a grid structure with defined rows and columns to help organise the project and frontend UI. It comes with pre-designed components like navigation bars, dropdowns, forms, and buttons that speed up development and ensure a consistent and modern design across different browsers and devices. 

2. Back-end:
- Django provideds a skeleton structure that has built in User models, admin backend and settings that assist in speeding up the development of a project. It is a web framework, acts as the middleware in a full-stack application and manages the communication between the frontend and the database. It plays a crucial role in handling requests from the frontend, processing data, and returning the appropriate responses. When a user interacts with the frontend of the website—say, by submitting a form or clicking a button—this action triggers an HTTP request. This request is sent to a URL, which Django maps to a specific view function through its URL dispatcher.

- The view function, written in Python, handles the request and performs the necessary operations. It might fetch or update data in the database, or execute other logic based on the request's details, it will generate receipts and load pages. Django uses an Object-Relational Mapper (ORM) to interact with the database, which provides a high-level, Pythonic interface for database queries. Django also used Jinja templating and template rendering similar to Flask, however an advantage to Django is it has a lot more built in security, with pre-made functions fo ruser authentication and password hashing. This means data can be manipulated in Python without writing SQL code. Once the view has processed the request, it constructs an HTTP response, often rendering an HTML template with context data. This context data is the information fetched or processed from the database, which is then incorporated into the HTML sent back to the frontend. This cycle of request and response 
enables a dynamic interaction between the user and the server, allowing the website to serve personalized and interactive content.

3. Databases:
- The postgreSQL database stores all of your data such as user information, available artworks, and orders—in tables with predefined schemas/models defined in Django. Different tables will cater to the different aspects of the website, such as storing login details for users, the specifc art items and shipping details.

## Section 4 – Bugs and Testing

Validators:

Bugs:
- This bug was stopping builds of the project being built, it does recognise the import module.
![image](https://github.com/JackAlexanderClark/VideoGames_eCommerce/assets/97599832/234d5444-2cd1-4bea-8e3e-e9ffd03d85c7)


Manual Testing (Unit Testing):

## Credits and Code Sources
I have used some front-end prepared templates from CodePen:

- Stripe API Code: https://stripe.com/gb
- Codepen:

