import React from 'react';

const defaultVal = { keyword: (window as any)['keywords']} //Insert the default value here.
export const SearchContext = React.createContext(defaultVal);