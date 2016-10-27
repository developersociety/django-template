module.exports = function(grunt, data) {
  return {
    // reloads browser on save
    options: {
      livereload: true,
    },

    less: {
      files: [data.lessDir + '/**/*.less',],
      tasks: ['default'],
      options: {
        livereload: true,
      }
    },
  };
};
