module.exports = function(grunt, data){
  return {
    development: {
      options: {
        paths: [data.cssDir],
        sourceMap: true,
        sourceMapURL: 'styles.css.map'
      },
      files: [{
        src: data.defaultLess,
        dest: data.defaultCss,
      }],
    },
  };
};
