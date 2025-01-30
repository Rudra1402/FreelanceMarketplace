import React from 'react';

const MarketplaceItemCard = ({ title, price }) => {
  return (
    <div className="rounded-lg shadow-lg bg-gray-800 hover:bg-blue-500 transition transform hover:-translate-y-2 duration-300 p-6">
      <h3 className="text-2xl font-semibold text-blue-300">{title}</h3>
      <p className="text-gray-300 mt-2">Price: {price}</p>
      <div className="mt-4 flex space-x-4">
        <button className="px-4 py-2 bg-blue-400 text-white rounded-lg hover:bg-blue-600 transition">
          View Details
        </button>
        <button className="px-4 py-2 bg-yellow-400 text-white rounded-lg hover:bg-yellow-500 transition">
          Edit
        </button>
        <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
          Delete
        </button>
      </div>
    </div>
  );
};

export default MarketplaceItemCard;
