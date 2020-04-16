import React from 'react';
import './PdfPlugin.css';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import { sourcePathPref } from './utils.js'

class PdfPlugin extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            numPages: undefined,
            pageNumber: 1
        }
        pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
    }

    onDocumentLoadSuccess = ({ numPages }) => {
        this.setState({ numPages });
    }

    changeToPrevPage() {
        let currentPageNumber = this.state.pageNumber;
        this.setState({ pageNumber: currentPageNumber - 1 });
    }

    changeToNextPage() {
        let currentPageNumber = this.state.pageNumber;
        this.setState({ pageNumber: currentPageNumber + 1 });
    }

    changePage() {
        let targetPage = parseInt(this.pageNumInput.value);
        if (targetPage > 0 && targetPage <= this.state.numPages) {
            this.setState({ pageNumber: targetPage });
        }
    }

    render() {
        let pdfFile = sourcePathPref + this.props.sourcePath;
        let jumpBar = this.state.numPages !== undefined
            ? <div className="jumpBar">
                Page:
                <input className="jumpBarInput text-center" type="text"
                    ref={(pageNumInput) => { this.pageNumInput = pageNumInput }} />&#91;1-{this.state.numPages}&#93;
                <span className="jumpBarGo unselectable cursorpointer" onClick={() => this.changePage()} >Go</span>
            </div>
            : undefined;
        let leftSwitch = (this.state.numPages !== undefined && this.state.pageNumber > 1)
            ? <div className="pdfViewerSwitcher unselectable cursorpointer pdfViewerSwitcherLeft"
                onClick={() => this.changeToPrevPage()} > Prev</div>
            : undefined;
        let rightSwitch = (this.state.numPages !== undefined && this.state.pageNumber < this.state.numPages)
            ? <div className="pdfViewerSwitcher unselectable cursorpointer pdfViewerSwitcherRight"
                onClick={() => this.changeToNextPage()}>Next</div>
            : undefined;

        return (
            <div className="columnListWrapper">
                {jumpBar}
                <Document className="pdfViewer" file={pdfFile} onLoadSuccess={this.onDocumentLoadSuccess}>
                    <Page pageNumber={this.state.pageNumber} />
                </Document>
                {leftSwitch}
                {rightSwitch}
                <p>Page {this.state.pageNumber} of {this.state.numPages}</p>
            </div>
        );
    }
}

export { PdfPlugin }