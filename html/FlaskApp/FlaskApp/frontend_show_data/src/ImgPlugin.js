import React from 'react';
import Zmage from 'react-zmage'
import { sourcePathPref } from './utils.js'

class ImgPlugin extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            numPages: undefined,
            pageNumber: 1
        }
    }

    render() {
        if (this.props.source === undefined
            || Object.prototype.toString.call(this.props.source) !== "[object Array]"
            || this.props.source.length === 0) {
            return (null);
        }

        let ZmageSrc = sourcePathPref + this.props.source[0];
        let ZmageSet = undefined;
        if (this.props.source.length > 1) {
            ZmageSet = [];
            for (let item of this.props.source) {
                ZmageSet.push({ src: sourcePathPref + item, alt: item });
            }
        }

        return (
            <div className="columnListWrapper">
                <p>Click to view all images.</p>
                <Zmage src={ZmageSrc} alt="Image" set={ZmageSet} zIndex={1030}
                    backdrop="linear-gradient(90deg, transparent 0%, lightgrey 100%)" />
            </div>
        );
    }
}

export { ImgPlugin }