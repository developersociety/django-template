module.exports = function(grunt, data) {
  return {

    // reloads browser on save
    options: {
      livereload: true,
    },

    less: {
      files: [data.lessDir + '/**/*.less',],
      tasks: ['less:development', 'autoprefixer', 'cssmin',],
      options: {
        livereload: true,
      }
    },

  };
};
