module.exports = function(grunt) {
    staticDir = './static';

    cssDir = staticDir + '/css';
    lessDir = staticDir + '/less';

    defaultCss = cssDir + '/styles.css';
    defaultCssMin = cssDir + '/styles.min.css';
    defaultLess = lessDir + '/styles.less';
    defaultCssMapName = 'styles.css.map';

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
