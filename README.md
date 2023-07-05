# Milestone Project 4 – Full-Stack Web Application

## Django Project

Title: Gallery of the Future

Author: Jack Clark

Email: jackalexanderclark@protonmail.com

Website link:

Contents:

## Section 1: Introduction

For my fourth milestone project I have built a Django application in the Pycharm IDE, that utilises several applications such as the gallery, shipping and authentication.

It uses AI generated art-work, using the cutting edge DALLE-2 (https://openai.com/dall-e-2), it can creates images from human text prompts. Attributes such as styles can be applied to mimic artists or effects.

Similar, to CHAT-GPT another OpenAI product it is trained on large quantities of images.

*** explain how it is trained using internet information

## Section 2: Project Design and Planning

- The project is a fictional art gallery using AI generated artwork. Users will be able to register an account, login and then browse the homepage which details the ethos and how DALLE-2 works.

- From there Users will be able to view the gallery with contains a variety of artwork, by hovering over and selecting a piece from the gallery – they can choose the piece they want and add it to their shopping basket. The quantities can be edited if they want multiple copies.

- After the User has selected the items they wish to purchase, they are then taken to the shipping section.

- Users can enter their shipping details and their card payments which are stored in their respective SQL models, the payments are handled using the third party “Stripe” API.

- Once the user has chosen their shipping destination, entered their banking details and the shipping speed.

- An order and receipt is generated which is stored within their profile, so they can track all their orders and their statuses.

## Section 4 – Bugs and Testing
