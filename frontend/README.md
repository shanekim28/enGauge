# Project enGauge
This is part of a project for the hackathon SD Hacks 2021. More information can be found on it [here](https://devpost.com/software/327267). 
This repository contains the front-end for displaying information collected by [this Discord bot](https://github.com/Sumadhwa13/teamtimtams/tree/master/bot).
It uses Angular 10 Material, [ngx-datatable](https://github.com/swimlane/ngx-datatable) and [ngx-charts](https://github.com/swimlane/ngx-charts).

## How to run it
You will need Node Package Manager in order to run this. You will also need the Angular CLI, which can be installed with the terminal command `npm install -g @angular/cli`. 
After you have cloned this directory, navigate into it and run  `npm install`. Then run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.
The app will only function if you have disabled same-origin-policy in your browser. For Chrome, instructions on doing so can be found [here](https://stackoverflow.com/questions/3102819/disable-same-origin-policy-in-chrome).
If you cannot disable the same-origin-policy or run into other issues, try commenting out line 39 and uncommenting line 40 in `/src/app/app.component.ts` to use locally-stored data instead of data from the server.

<!--## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).-->
