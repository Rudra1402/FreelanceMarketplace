import React, { useState } from 'react';
import MarketplaceItemCard from '../components/Marketplace/MarketplaceItemCard';
import NewMarketplaceItemForm from '../components/Marketplace/NewMarketplaceItemForm';

const Marketplace = () => {
  const [showFormModal, setShowFormModal] = useState(false);

  const sampleItems = [
    { id: 1, title: 'Handmade Wooden Table', description: 'Beautifully crafted.', price: '$200 - $500' },
    { id: 2, title: 'Modern Desk Lamp', description: 'Perfect for your workspace.', price: '$50 - $100' },
    { id: 3, title: 'Gaming Chair', description: 'Ergonomic and stylish.', price: '$150 - $300' },
  ];

  return (
    <div className="min-h-screen min-w-screen flex flex-col justify-start items-center text-white p-6">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-6 w-[90%]">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 text-transparent bg-clip-text">Marketplace</h1>
        <button
          onClick={() => setShowFormModal(true)}
          className="px-4 py-2 bg-green-500 text-white font-medium rounded-lg shadow shadow-gray-500 hover:bg-green-600 transition"
        >
          Add New Item
        </button>
      </div>

      {/* Marketplace Items */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {sampleItems.map((item) => (
          <MarketplaceItemCard
            key={item.id}
            title={item.title}
            description={item.description}
            price={item.price}
          />
        ))}
      </div>

      {/* Modal for Adding New Item */}
      {showFormModal && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white w-11/12 max-w-lg p-4 rounded-lg shadow-lg relative">
            <button
              onClick={() => setShowFormModal(false)}
              className="absolute top-6 right-6 !bg-gray-100 text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
            <NewMarketplaceItemForm />
          </div>
        </div>
      )}
    </div>
  );
};

export default Marketplace;
