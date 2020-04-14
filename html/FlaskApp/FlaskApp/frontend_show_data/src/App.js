import React from 'react';
import { Table, Tag } from 'antd';
import './App.css';

const renderStrategySet = {
  linable: text => <a>{text}</a>,
  colorTags: tags => (
    <span>
      {tags.map(tag => {
        let color = tag.length > 5 ? 'geekblue' : 'green';
        if (tag === 'loser') {
          color = 'volcano';
        }
        return (
          <Tag color={color} key={tag}>
            {tag.toUpperCase()}
          </Tag>
        );
      })}
    </span>
  ),
  inviteAndDelete: (text, record) => (
    <span>
      <a style={{ marginRight: 16 }}>Invite {record.name}</a>
      <a>Delete</a>
    </span>
  )
};

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userName: '',
      datasetName: '',
      columns: undefined,
      data: undefined
    }
  }

  handleTable(jsonData) {
    if (jsonData.columns && jsonData.data) {
      let columnsD = jsonData.columns;
      for (let column of columnsD) {
        column.render = renderStrategySet[column.renderStrategy];
      }
      this.setState({ columns: columnsD, data: jsonData.data });
    }
  }

  componentDidMount() {
    console.log("fetching python localhost");
    fetch('http://localhost:8080/show_data_fetch', {
      method: 'GET',
      mode: 'no-cors',
      dataType: 'json'
    }).then(res => res.json()).then(res => {
      console.log(res)
      this.setState({ userName: res.username, datasetName: res.datasetName });
      if (res.type === 'table') {
        this.handleTable(res);
      }
    }).catch(err => console.log(err))
  }

  render() {
    return (
      <div className="App">
        <nav className="navbar" id="mainNav">
          <div className="nav-container">
            <a className="navbar-brand" href="dashboard">Aggie STEM</a>
            <div className="navbar-collapse">
              <ul className="navbar-nav">
                <li className="nav-item" id="login" name="login">
                  <a className="nav-link" href="user_profile">{this.state.userName}</a>
                </li>
                <li className="nav-item" id="logout" name="logout">
                  <a className="nav-link" href="logout">Logout</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="mainBody">
          <h1 className="datasetName">Current Dataset: {this.state.datasetName}</h1>
          <Table columns={this.state.columns} dataSource={this.state.data} />
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
