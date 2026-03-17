CXX ?= g++
CXXFLAGS ?= -Wall -Wextra -Werror -I..

TEST_SRC = test_midea_dehum.cpp
TEST_BIN = run_tests

all: test

test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(TEST_SRC) ../components/midea_dehum/midea_dehum_utils.h
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(TEST_BIN)
