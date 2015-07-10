module.exports = function(grunt, data) {
  return {
    options: {
      sourceMap: true,
    },
    build: {
      files: [{
        src: [
          staticDir + '/css/!(default.min.css)*.css',
        ],
        dest: defaultCssMin,
      }],
    },
  };
};
