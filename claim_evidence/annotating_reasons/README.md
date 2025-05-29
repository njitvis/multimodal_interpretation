# UI for Annotating Reasoning Strategies

This project is a React-based web application. Follow the instructions below to set up, run, and build the application on your local machine.

## 📦 Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v14 or higher recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js) or [Yarn](https://yarnpkg.com/)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/njitvis/multimodal_interpretation.git
cd multimodal_interpretation/claim_evidence/annotating_reasons
````

### 2. Checkout the Correct Branch

Make sure you are on the `annotating_reasoning_strategy` branch:

```bash
git checkout annotating_reasoning_strategy
```

### 3. Install Dependencies

Using npm:

```bash
npm install
```

Or using yarn:

```bash
yarn install
```

### 4. Start the Development Server

Using npm:

```bash
npm start
```

Or using yarn:

```bash
yarn start
```

This will start the app on [http://localhost:3000](http://localhost:3000)

## 🖼️ Chart Images Requirement
For the application to display charts correctly after loading a JSON file, all chart images must be placed in the public/ folder.
Each image file name must exactly match its corresponding <image_id>.png (e.g., 12345.png) as referenced in the JSON.

❗ If the images are missing or incorrectly named, the charts will not render properly in the app.

## 📁 Project Structure

```
annotating_reasons/
├── public/            # chart images (e.g., 123.png, 456.png)
├── src/               # Source code
│   ├── components/    # Reusable components
│   ├── App.js         # Main app component
│   └── index.js       # Entry point
├── package.json       # Project metadata and scripts
└── README.md
```
