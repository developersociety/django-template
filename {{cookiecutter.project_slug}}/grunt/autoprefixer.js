module.exports = function(grunt, data) {
  return {
    options: {
      map: {
        prev: true,
        inline: false,
        annotation: 'styles.css.map',
      },
      expand: true,
      flatten: true,
    }, //build
    single_file: {
      src: data.defaultCss,
      dest: data.defaultCss,
    }
  };
};
