#include <vector>


// I would like to write a container that allows me to build up an object such as an std::vector, but once it is built up I can only access it through a const reference
template <typename T>
class ImmutableVector {
public:
	ImmutableVector() = default;
	ImmutableVector(const ImmutableVector&) = default;
	ImmutableVector(ImmutableVector&&) = default;
	ImmutableVector& operator=(const ImmutableVector&) = default;
	ImmutableVector& operator=(ImmutableVector&&) = default;
	~ImmutableVector() = default;

	/* Methods allowed on object in building stage */
	void push_back(const T& value){
		this->assert_not_built();
		_data.push_back(value);
	}

	void push_back(T&& value) {
		this->assert_not_built();
		_data.push_back(std::move(value));
	}

	T& operator[](std::size_t i) {
		this->assert_not_built();
		this->assert_valid_index(i);
		return _data[i];
	}

	void erase(std::size_t i) {
		this->assert_not_built();
		this->assert_valid_index(i);
		_data.erase(_data.begin() + i);
	}

	void clear() {
		this->assert_not_built();
		_data.clear();
	}

	typename std::vector<T>::iterator begin() {
		this->assert_not_built();
		return _data.begin();
	}

	typename std::vector<T>::iterator end() {
		this->assert_not_built();
		return _data.end();
	}

	void mark_built() {
		this->assert_not_built();
		_built = true;
	}

	/* Methods allowed on all object, both in building stage and built */
	const T& operator[](std::size_t i) const {
		this->assert_valid_index(i);
		return _data[i];
	}

	typename std::vector<T>::const_iterator begin() const {
		return _data.cbegin();
	}

	typename std::vector<T>::const_iterator end() const {
		return _data.cend();
	}

	typename std::vector<T>::const_iterator cbegin() const {
		return _data.cbegin();
	}

	typename std::vector<T>::const_iterator cend() const {
		return _data.cend();
	}

	std::size_t size() const {
		return _data.size();
	}

private:
	std::vector<T> _data;
	bool _built = false;

	void assert_not_built() const {
		if (_built)
			throw std::runtime_error("ImmutableVector is already built");
	}

	void assert_built() const {
		if (!_built)
			throw std::runtime_error("ImmutableVector is not built");
	}

	void assert_valid_index(std::size_t i) const {
		if (i >= _data.size())
			throw std::out_of_range("Index out of range");
	}
};
