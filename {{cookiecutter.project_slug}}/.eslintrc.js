module.exports = {
    extends: ['airbnb-base', 'plugin:prettier/recommended'],
    parserOptions: {
        ecmaVersion: 13,
    },
    rules: {
        indent: ['error', 4, { SwitchCase: 1 }],
        camelcase: [0],
        'one-var': [0],
        'no-new': [0],
        'no-param-reassign': [2, { props: false }],
        'operator-linebreak': ['error', 'after'],
        'import/no-extraneous-dependencies': [
            'error',
            {
                devDependencies: true,
            },
        ],
        'prefer-destructuring': [
            'error',
            {
                array: false,
                object: false,
            },
        ],
    },
    env: {
        browser: true,
        node: true,
    },
};
