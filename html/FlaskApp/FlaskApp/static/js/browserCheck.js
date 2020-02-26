function isMobileDevice() {
  return (/iPhone|iPod|iPad|Android|BlackBerry|Kindle|RIM|Mobile/).test(navigator.userAgent);
}

function isUnsupportedBrowserVersion() {
  // With IE 9.0 and 10.0 the site will load but most functionality will not be there (e.g. viewing or even selecting files)
  const isUnsupportedIEVersion = (
    navigator.appName === 'Microsoft Internet Explorer' &&
    (navigator.appVersion.indexOf(' MSIE 9.0;') > -1 ||
      navigator.appVersion.indexOf(' MSIE 10.0;') > -1)
  );
  var isUnsupportedNonIEVersion = false;
  const isSafari = (navigator.userAgent.indexOf('Safari') !== -1 && navigator.userAgent.indexOf('Chrome') === -1);
  if (isSafari) {
    const version = navigator.appVersion.match(/Version\/(.*?) /);
    if (version && version.length > 1) {
      const versionNum = parseFloat(version[1]);
      if (versionNum < 7.1) {
        isUnsupportedNonIEVersion = true;
      }
    }
  }

  return isUnsupportedIEVersion || isUnsupportedNonIEVersion;
}

function isUnknownBrowser() {
  return !((/Chrome|Safari|Gecko/).test(navigator.appVersion) || (/Gecko/).test(navigator.product)) &&
    !localStorage.xodoContinue;
}

// This check fails on IE < 9.0  If this fails the site will not even load
if (typeof Array.isArray === 'undefined') {
  window.location.href = 'oldbrowser.html';
} else if (isMobileDevice()) {
  // if we're on the collab page (aka public link) then we shouldn't redirect for mobile devices
  // since it will be handled automatically by the component
  /*if (window.location.hash.indexOf('#/collab') !== 0) {
    window.location.href = 'mobile.html';
  }*/
} else if (isUnsupportedBrowserVersion()) {
  window.location.href = 'oldbrowser.html';
} else if (isUnknownBrowser()) {
  window.location.href = 'unknownbrowser.html';
}
