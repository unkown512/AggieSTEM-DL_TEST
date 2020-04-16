import React from 'react';
import { Table, Tag } from 'antd';
import { sourcePathPref } from './utils.js'

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


class TablePlugin extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            dataSource: undefined,
            columns: undefined
        }
    }

    componentDidMount() {
        if (this.props.type === 'csv') {
            fetch(sourcePathPref + this.props.sourcePath)
                .then(res => res.text())
                .then(text => {
                    text = text.split(/\n/);
                    let isColumns = true, dataSourceD = [], columnsD = [];
                    for (let item of text) {
                        if (item.length === 0) { continue; }
                        item = item.trim().match(/("[^"]+"|[^,]+)/g);
                        if (isColumns === true) {
                            for (let columnName of item) {
                                columnsD.push({
                                    'title': columnName,
                                    'dataIndex': columnName,
                                    'key': columnName,
                                });
                            }
                            isColumns = false;
                        } else {
                            let rowData = {}, elementCount = 0;
                            for (let rowElement of item) {
                                if (elementCount === columnsD.length) { break; }
                                rowData[columnsD[elementCount]['key']] = rowElement;
                                elementCount++;
                            }
                            dataSourceD.push(rowData);
                        }
                    }
                    this.setState({ dataSource: dataSourceD, columns: columnsD })
                });
        } else if (this.props.type === 'table') {
            let columnsD = this.props.columns;
            for (let column of columnsD) {
                column.render = renderStrategySet[column.renderStrategy];
            }
            this.setState({ dataSource: this.props.dataSource, columns: columnsD })
        }
    }

    render() {
        return (
            <div className="columnListWrapper">
                <Table style={{ width: "100%" }} dataSource={this.state.dataSource} columns={this.state.columns} />;
            </div>
        );
    }
}

export { TablePlugin }