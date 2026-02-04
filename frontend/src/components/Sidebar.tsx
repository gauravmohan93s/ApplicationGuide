import React, { useState, useEffect } from 'react';
import { Filters } from '../api';

interface SidebarProps {
    onFilterChange: (filters: Filters) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onFilterChange }) => {
    const [filters, setFilters] = useState<Filters>({});

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target;
        setFilters(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : (value ? Number(value) : undefined)
        }));
    };

    useEffect(() => {
        const timeoutId = setTimeout(() => {
            onFilterChange(filters);
        }, 500); // Debounce
        return () => clearTimeout(timeoutId);
    }, [filters, onFilterChange]);

    return (
        <div className="w-64 bg-gray-50 p-4 border-r border-gray-200 h-screen overflow-y-auto fixed left-0 top-0">
            <h2 className="text-xl font-bold mb-6 text-indigo-700">Filters</h2>
            
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Min GPA (UG)</label>
                <input
                    type="number"
                    name="min_gpa"
                    step="0.1"
                    placeholder="e.g. 6.0"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    onChange={handleChange}
                />
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Max Tuition (GBP)</label>
                <input
                    type="number"
                    name="max_tuition"
                    placeholder="e.g. 15000"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    onChange={handleChange}
                />
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Max IELTS Score</label>
                <input
                    type="number"
                    name="ielts_score"
                    step="0.5"
                    placeholder="e.g. 6.5"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    onChange={handleChange}
                />
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Max Backlogs</label>
                <input
                    type="number"
                    name="backlogs"
                    placeholder="e.g. 5"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                    onChange={handleChange}
                />
            </div>

            <div className="mb-4 flex items-center">
                <input
                    type="checkbox"
                    name="is_stem"
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    onChange={handleChange}
                />
                <label className="ml-2 block text-sm text-gray-900">STEM Only</label>
            </div>
        </div>
    );
};

export default Sidebar;
