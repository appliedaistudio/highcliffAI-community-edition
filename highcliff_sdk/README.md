<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="left">
  <h1 align="left">appliedAIstudio</h1>
</div>
<br />


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#naming-conventions">Naming Conventions</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#quick-start">Quick Start</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>




<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Describe the purpose of the project, but do so by answering two questions.  What components will be up and running when the code is run properly? What will the code do when it's up and running? The reader wants to know what will (or should) get launched, and what will (or should) it do.

Give the reader a diagram and walk them through it. The diagram should be a UML development view like the one shown above. UML is simple to understand and most readers have already had experience with them. The above diagram is much more complicated that what you will typically have. Typically, the diagram will be some subset of the system depicted. So it may only show user-interface components or a single data pipeline.

The diagram should be a specific implementation of the general systems architecture for appliedAIstudio solutions. Diagrams for your project should derived from the more general diagrams in the [general solution architectre](https://github.com/appliedaistudio/solution-architecture).

Let the diagram do most of the work. The diagram should be clear enough for the reader to understand most of the intended solution.  Use this text to give the reader a brief tour of the diagram and to disclose any details that are not easy to express in the UML diagram. The tour should follow the information flow of the system. Where does information start? Where does it go next? Where does it end? Bullet points or lists are a good way to describe what the system is intended to do. For example:

* The system takes in resume data
* It also takes in job postings
* It matches resumes to job posts and records the match score

You should also describe how each file corresponds to each element shown in the diagram. As you describe each element in the diagram, name the file in the repository that contains the code for that element. For example, you could say something like;

The ML model is implemented in `ml.py`

Be sure to do this for every element shown in the diagram.

<p align="right">(<a href="#top">back to top</a>)</p>



### Naming Conventions

This project uses the following naming conventions for repos, directories, files,  commits, versions, and programming lanuages. 

#### Repos

Repos will use kebab case with all lower case letters and no other special characters. Numbers are allowed. Related repos can be found filtering on  the product/project name. 

```
[product/project name]-[purpose]-[subpurpose] e.g. solution-devops-templaterepo
```

Repos names will be:

- Descriptive
- Readable
- Consistent
- Contextual
- Future-friendly
- Extensible
- Reusable
- Brief (short/ succinct)

Repo name guidelines adapted from  the [British Columbia Policy Framework for GitHub Document Naming Repos](https://github.com/bcgov/BC-Policy-Framework-For-GitHub/blob/master/BC-Gov-Org-HowTo/Naming-Repos.md).

#### Directories

Directories use the same conventions as repos with the exception that leading periods (.) and underscores (_) can be used. Directories do not have to have multple name sections separated by dashes.

#### Files

File names follow the same name guidelines as repos and directories and have no spaces.

#### Commits

Commits use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#specification).

**ex:**

```
docs(readme): update readme with examples
feat(api)!: add pagination to results
fix(frontend): fix tab order on form fields
```

#### Versions

Release versions use [Semantic Versioning](https://semver.org/), with the version number prefixed with "v'".

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> 1. MAJOR version when you make incompatible API changes,
> 2. MINOR version when you add functionality in a backwards compatible manner, and
> 3. PATCH version when you make backwards compatible bug fixes.
>
> Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

**ex:**

```
v1.0.11
v1.5.0
v2.1.3
```



#### Programming Languages

Code will use the most widely excepted sytle guide for a particular programming language with development begins. e.g. [PEP8](https://www.python.org/dev/peps/pep-0008/) for Python.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

The purpose is to let the reader know what kind of background information they will need to understand this solution. Imagine someone technically competent, but new to this project. What technologies would be helpful to read up on? What background reading did you wish you had when you started this project? In the introductory paragraph, describe the general purpose for each technology listed. Answer the question: what would happen if that technology was missing? List each technology below with a link to background information for the reader. Here are a few examples.

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The worst part of a GitHub project is staring at folders and code and wondering: what now? Give the reader a basic overview of how to turn the code in this repository into a working system. The _Quick Start_ section will give step-by-step instructions. Here you should describe the basic ideas. You want to give the reader a mental model of how to set things up so that when they read through the detailed instructions, they can put each step into a meaningful context. This section should describe the basic ideas behind the quick start process in enough detail so that someone reading through the steps in the _Quick Start_ section could tell if there was a step missing or out of order.

If this project, for example, were instructions on building a house. You would describe the general idea of putting in the foundation, then framing out the building, putting in the infrastructure, then finishing off the walls. These aren't detailed steps, but a general description for understanding detailed steps later.

### Prerequisites

Assume the reader is starting with commodity compute and storage technology. Walk the reader through the prerequisites of preparing the standard environment for running this system. For each step, start be describing why that step is necessary (what will happen if they decide to skip this step). Give a bullet point with a very short description of the step. Follow that with a code block that describes the system interactions needed to achieve that step. For example:

The user interface is a Node JavaScript application. You will need to install Node to run the dashboard user interface. 
* npm
  ```sh
  npm install npm@latest -g
  ```

### Quick Start
These are the minimum steps needed to get a copy of the system up and running.
_Below is an example of how you can instruct your audience on installing and setting up your app. Spend a considerable amount of time making these instructions as short as possible._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
This section is extremely important. Do not delete this, skip this, or leave it blank. Create content similar to the example below. Update this section regularly.

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing
_Keep this section only if the project is open source..._

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Team Member, Role - email@example.com<br/>
Team Member, Role - email@example.com<br/>
Team Member, Role - email@example.com<br/>
Team Member, Role - email@example.com<br/>
Team Member, Role - email@example.com<br/>


Project Link: [https://github.com/your_org/repo_name](https://github.com/your_org/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/UMLdevelopmentview_appliedaistudio_v1_20220117.png
