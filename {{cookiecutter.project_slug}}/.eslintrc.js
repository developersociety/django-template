module.exports = {
    extends: ['airbnb-base', 'plugin:prettier/recommended'],
    rules: {
        indent: ['error', 4],
        camelcase: [0],
        'one-var': [0],
        'no-new': [0],
        'comma-dangle': ['error', 'never'],
        'no-param-reassign': [2, { props: false }],
        'operator-linebreak': ['error', 'after'],
        'import/no-extraneous-dependencies': [
            'error',
            {
                devDependencies: true
            }
        ],
        'prefer-destructuring': [
            'error',
            {
                array: false,
                object: false
            }
        ]
    },
    env: {
        browser: true,
        node: true
    }
};
