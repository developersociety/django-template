module.exports = function(grunt) {
    var staticDir = './static';

    var cssDir = staticDir + '/css';
    var lessDir = staticDir + '/less';

    var defaultCss = cssDir + '/styles.css';
    var defaultCssMin = cssDir + '/styles.min.css';
    var defaultLess = lessDir + '/styles.less';

    require('load-grunt-config')(grunt, {
        data: {
            cssDir: cssDir,
            defaultCss: defaultCss,
            defaultCssMin: defaultCssMin,
            defaultLess: defaultLess,
            lessDir: lessDir,
            staticDir: staticDir,
        }
    });
};
