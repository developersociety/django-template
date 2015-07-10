module.exports = function(grunt) {

PROJECT_NAME = '{{ project_name }}';

rootDir = '/var/www/' + PROJECT_NAME;
staticDir = rootDir + '/static';

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
