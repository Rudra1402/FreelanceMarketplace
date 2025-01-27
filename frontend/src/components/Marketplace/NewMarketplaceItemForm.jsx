import React from 'react';

const NewMarketplaceItemForm = () => {
  return (
    <form>
      <h2>Create New Item</h2>
      <input type="text" placeholder="Item Title" />
      <textarea placeholder="Description"></textarea>
      <input type="number" placeholder="Min Price" />
      <input type="number" placeholder="Max Price" />
      <button type="submit">Submit</button>
    </form>
  );
};

export default NewMarketplaceItemForm;
