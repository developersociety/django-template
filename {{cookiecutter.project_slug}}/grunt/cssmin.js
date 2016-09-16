module.exports = function(grunt, data) {
  return {
    options: {
      sourceMap: true,
    },
    build: {
      files: [{
        src: data.defaultCss,
        dest: defaultCssMin,
      }],
    },
  };
};
