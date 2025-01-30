import React from 'react';

const NewMarketplaceItemForm = () => {
  return (
    <div className='min-h-full min-w-full flex flex-col justify-center items-center text-white'>
      <form className="bg-gray-800 text-white rounded-lg shadow-lg p-8 w-full">
        <h2 className="text-3xl font-bold text-blue-400 mb-6">Create New Item</h2>
        <input
          type="text"
          placeholder="Item Title"
          className="w-full p-3 rounded-lg bg-gray-700 text-gray-300 mb-4"
        />
        <textarea
          placeholder="Description"
          className="w-full p-3 rounded-lg bg-gray-700 text-gray-300 mb-4"
        ></textarea>
        <div className="flex space-x-4 mb-4">
          <input
            type="number"
            placeholder="Min Price"
            className="w-full p-3 rounded-lg bg-gray-700 text-gray-300"
          />
          <input
            type="number"
            placeholder="Max Price"
            className="w-full p-3 rounded-lg bg-gray-700 text-gray-300"
          />
        </div>
        <button
          type="submit"
          className="w-full p-3 bg-blue-500 rounded-lg text-white font-semibold hover:bg-blue-600 transition"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default NewMarketplaceItemForm;
