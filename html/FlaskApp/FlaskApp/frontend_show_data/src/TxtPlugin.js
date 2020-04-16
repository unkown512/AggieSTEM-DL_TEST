import React from 'react';
import { sourcePathPref } from './utils.js'

class TxtPlugin extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className="columnListWrapper">
                <iframe name="frmMain" src={sourcePathPref + this.props.sourcePath} id="frmMain" width="100%" height="600px" ></iframe>
            </div>
        );
    }
}

export { TxtPlugin }