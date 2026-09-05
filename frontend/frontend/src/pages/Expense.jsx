import { useEffect, useState } from "react";
import api from "../service/api";

function Expenses() {
    const [expenses, setExpenses] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [showForm, setShowForm] = useState(false);

    const [form, setForm] = useState({
        amount: "",
        category: "",
        description: "",
        expense_date: ""
    });

    const [editingId, setEditingId] = useState(null);

    // Filters
    const [category, setCategory] = useState("");
    const [search, setSearch] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [minAmount, setMinAmount] = useState("");
    const [maxAmount, setMaxAmount] = useState("");

    const loadExpenses = async () => {
        try {
            setLoading(true);

            const params = {};

            if (category) {
                params.category = category;
            }

            if (search) {
                params.search = search;
            }

            if (startDate) {
                params.start_date = startDate;
            }

            if (endDate) {
                params.end_date = endDate;
            }

            if (minAmount) {
                params.min_amount = minAmount;
            }

            if (maxAmount) {
                params.max_amount = maxAmount;
            }

            const response = await api.get(
                "/expenses",
                { params }
            );

            setExpenses(response.data);
            setError("");

        } catch (error) {
            console.error(
                "Expense loading error:",
                error
            );

            setError(
                "Unable to load expenses."
            );

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadExpenses();
    }, [
        category,
        search,
        startDate,
        endDate,
        minAmount,
        maxAmount
    ]);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {

            const data = {
                amount: Number(form.amount),
                category: form.category,
                description: form.description,
                expense_date: form.expense_date
            };

            if (editingId) {

                await api.put(
                    `/expenses/${editingId}`,
                    data
                );

            } else {

                await api.post(
                    "/expenses",
                    data
                );
            }

            setForm({
                amount: "",
                category: "",
                description: "",
                expense_date: ""
            });

            setEditingId(null);
            setShowForm(false);

            loadExpenses();

        } catch (error) {

            console.error(
                "Save expense error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Unable to save expense."
            );
        }
    };

    const handleEdit = (expense) => {

        setForm({
            amount: expense.amount,
            category: expense.category,
            description: expense.description,
            expense_date: expense.expense_date
        });

        setEditingId(expense.id);
        setShowForm(true);
    };

    const handleDelete = async (id) => {

        const confirmed = window.confirm(
            "Are you sure you want to delete this expense?"
        );

        if (!confirmed) {
            return;
        }

        try {

            await api.delete(
                `/expenses/${id}`
            );

            loadExpenses();

        } catch (error) {

            console.error(
                "Delete error:",
                error
            );

            setError(
                "Unable to delete expense."
            );
        }
    };

    const clearFilters = () => {

        setCategory("");
        setSearch("");
        setStartDate("");
        setEndDate("");
        setMinAmount("");
        setMaxAmount("");
    };

    return (
        <div className="expenses-page">

            <div className="expenses-header">

                <div>
                    <h1>Expenses</h1>

                    <p>
                        Manage your expenses
                    </p>
                </div>

                <button
                    className="add-button"
                    onClick={() => {
                        setEditingId(null);

                        setForm({
                            amount: "",
                            category: "",
                            description: "",
                            expense_date: ""
                        });

                        setShowForm(true);
                    }}
                >
                    + Add Expense
                </button>

            </div>

            {error && (
                <div className="error">
                    {error}
                </div>
            )}

            {/* FILTERS */}

            <div className="filters">

                <input
                    type="text"
                    placeholder="Search description..."
                    value={search}
                    onChange={(e) =>
                        setSearch(e.target.value)
                    }
                />

                <input
                    type="text"
                    placeholder="Category"
                    value={category}
                    onChange={(e) =>
                        setCategory(e.target.value)
                    }
                />

                <input
                    type="date"
                    value={startDate}
                    onChange={(e) =>
                        setStartDate(e.target.value)
                    }
                />

                <input
                    type="date"
                    value={endDate}
                    onChange={(e) =>
                        setEndDate(e.target.value)
                    }
                />

                <input
                    type="number"
                    placeholder="Min amount"
                    value={minAmount}
                    onChange={(e) =>
                        setMinAmount(e.target.value)
                    }
                />

                <input
                    type="number"
                    placeholder="Max amount"
                    value={maxAmount}
                    onChange={(e) =>
                        setMaxAmount(e.target.value)
                    }
                />

                <button
                    onClick={clearFilters}
                >
                    Clear
                </button>

            </div>

            {/* FORM */}

            {showForm && (
                <div className="expense-form-card">

                    <h2>
                        {editingId
                            ? "Edit Expense"
                            : "Add Expense"}
                    </h2>

                    <form
                        onSubmit={handleSubmit}
                    >

                        <input
                            type="number"
                            step="0.01"
                            name="amount"
                            placeholder="Amount"
                            value={form.amount}
                            onChange={handleChange}
                            required
                        />

                        <input
                            type="text"
                            name="category"
                            placeholder="Category"
                            value={form.category}
                            onChange={handleChange}
                            required
                        />

                        <input
                            type="text"
                            name="description"
                            placeholder="Description"
                            value={form.description}
                            onChange={handleChange}
                            required
                        />

                        <input
                            type="date"
                            name="expense_date"
                            value={form.expense_date}
                            onChange={handleChange}
                            required
                        />

                        <div className="form-buttons">

                            <button type="submit">
                                {editingId
                                    ? "Update"
                                    : "Save"}
                            </button>

                            <button
                                type="button"
                                onClick={() => {
                                    setShowForm(false);
                                    setEditingId(null);
                                }}
                            >
                                Cancel
                            </button>

                        </div>

                    </form>

                </div>
            )}

            {/* EXPENSE LIST */}

            <div className="expense-list">

                {loading ? (

                    <p>
                        Loading expenses...
                    </p>

                ) : expenses.length === 0 ? (

                    <div className="empty-state">

                        <h2>
                            No expenses found
                        </h2>

                        <p>
                            Add your first expense
                            to get started.
                        </p>

                    </div>

                ) : (

                    expenses.map((expense) => (

                        <div
                            className="expense-card"
                            key={expense.id}
                        >

                            <div>

                                <h3>
                                    {expense.category}
                                </h3>

                                <p>
                                    {expense.description}
                                </p>

                                <small>
                                    {expense.expense_date}
                                </small>

                            </div>

                            <div className="expense-right">

                                <strong>
                                    ₹
                                    {Number(
                                        expense.amount
                                    ).toFixed(2)}
                                </strong>

                                <div>

                                    <button
                                        onClick={() =>
                                            handleEdit(
                                                expense
                                            )
                                        }
                                    >
                                        Edit
                                    </button>

                                    <button
                                        onClick={() =>
                                            handleDelete(
                                                expense.id
                                            )
                                        }
                                    >
                                        Delete
                                    </button>

                                </div>

                            </div>

                        </div>

                    ))
                )}

            </div>

        </div>
    );
}

export default Expenses;