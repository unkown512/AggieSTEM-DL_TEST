import React from 'react';
import './App.css';
import { urlPathPref } from './utils.js'
import { browserHistory } from 'react-router';
import { PdfPlugin } from './PdfPlugin.js';
import { ImgPlugin } from './ImgPlugin.js'
import { TablePlugin } from './TablePlugin.js'
import { TxtPlugin } from './TxtPlugin.js'
import axios from 'axios';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userName: '',
      datasetName: '',
      type: '',
      columns: undefined,
      data: undefined,
      sourcePath: undefined
    }
  }

  handleTable(jsonData) {
    if (jsonData.columns && jsonData.data) {
      this.setState({ type: 'table', columns: jsonData.columns, data: jsonData.data });
    }
  }

  handlePdf(jsonData) {
    if (jsonData.source) {
      this.setState({ type: 'pdf', sourcePath: jsonData.source });
    }
  }

  handleImg(jsonData) {
    if (jsonData.source) {
      this.setState({ type: 'img', sourcePath: jsonData.source });
    }
  }

  handleCsv(jsonData) {
    if (jsonData.source) {
      this.setState({ type: 'csv', sourcePath: jsonData.source });
    }
  }

  handleTxt(jsonData) {
    if (jsonData.source) {
      this.setState({ type: 'txt', sourcePath: jsonData.source });
    }
  }

  componentDidMount() {
    let filePost = browserHistory.getCurrentLocation().pathname;
    filePost = filePost.split('/')[filePost.split('/').length - 1];
    axios.post('http://localhost:8080/show_data/post', { "fileName": filePost })
      .then((res) => {
        let json = res.data;
        this.setState({ userName: json.username, datasetName: json.datasetName });
        if (json.type === 'table') {
          this.handleTable(json);
        } else if (json.type === 'pdf') {
          this.handlePdf(json);
        } else if (json.type === 'img') {
          this.handleImg(json);
        } else if (json.type === 'csv') {
          this.handleCsv(json);
        } else if (json.type === 'txt') {
          this.handleTxt(json);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  render() {
    let mainPlugin = undefined;
    if (this.state.type === 'pdf') {
      mainPlugin = <PdfPlugin sourcePath={this.state.sourcePath} />;
    } else if (this.state.type === 'img') {
      mainPlugin = <ImgPlugin source={this.state.sourcePath} />;
    } else if (this.state.type === 'csv') {
      mainPlugin = <TablePlugin type='csv' sourcePath={this.state.sourcePath} />;
    } else if (this.state.type === 'table') {
      mainPlugin = <TablePlugin type='table' columns={this.state.columns} dataSource={this.state.data} />;
    } else if (this.state.type === 'txt') {
      mainPlugin = <TxtPlugin sourcePath={this.state.sourcePath} />;
    }

    return (
      <div className="App">
        <nav className="navbar" id="mainNav">
          <div className="nav-container">
            <a className="navbar-brand" href={urlPathPref + "dashboard"}>Aggie STEM</a>
            <div className="navbar-collapse">
              <ul className="navbar-nav">
                <li className="nav-item" id="login" name="login">
                  <a className="nav-link" href={urlPathPref + "user_profile"}>{this.state.userName}</a>
                </li>
                <li className="nav-item" id="logout" name="logout">
                  <a className="nav-link" href={urlPathPref + "logout"}>Logout</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="mainBody">
          <h1 className="datasetName">Current Dataset: {this.state.datasetName}</h1>
          {mainPlugin}
        </div>

        <footer className="py-5 bg-dark">
          <div className="container">
            <p className="m-4 text-center text-dark">Copyright &copy; AggieSTEM 2019</p>
          </div>
        </footer>
      </div>
    );
  }
}

export { App };
